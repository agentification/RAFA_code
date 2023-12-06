

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(ontable c)
(ontable d)
(ontable e)
(on f c)
(on g d)
(ontable h)
(ontable i)
(clear a)
(clear b)
(clear e)
(clear f)
(clear h)
(clear i)
)
(:goal
(and
(on a h)
(on c e)
(on d i)
(on f g)
(on g c)
(on h b))
)
)


