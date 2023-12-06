

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d e)
(on e a)
(ontable f)
(on g c)
(on h b)
(ontable i)
(clear f)
(clear g)
(clear h)
(clear i)
)
(:goal
(and
(on b h)
(on d f)
(on e d)
(on f i)
(on g a)
(on i b))
)
)


