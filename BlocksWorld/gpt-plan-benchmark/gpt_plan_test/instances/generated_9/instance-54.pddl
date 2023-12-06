

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c e)
(on d i)
(ontable e)
(ontable f)
(ontable g)
(on h b)
(on i h)
(clear a)
(clear c)
(clear d)
(clear g)
)
(:goal
(and
(on b h)
(on c f)
(on d g)
(on e d)
(on h e)
(on i b))
)
)


